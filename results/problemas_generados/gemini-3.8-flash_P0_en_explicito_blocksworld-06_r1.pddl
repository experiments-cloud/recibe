(define (problem BLOCKS-6-0)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (handempty)
    (ontable b)
    (ontable c)
    (on a c)
    (on d a)
    (on e b)
    (on f e)
    (clear d)
    (clear f)
  )
  (:goal
    (and
      (on a e)
      (on b a)
      (on c b)
      (on e f)
      (on f d)
    )
  )
)
