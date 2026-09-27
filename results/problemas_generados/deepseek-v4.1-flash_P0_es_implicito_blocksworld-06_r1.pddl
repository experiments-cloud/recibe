(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (ontable b)
    (ontable c)
    (on e b)
    (on f e)
    (on a c)
    (on d a)
    (clear f)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on c b)
      (on b a)
      (on a e)
      (on e f)
      (on f d)
    )
  )
)
