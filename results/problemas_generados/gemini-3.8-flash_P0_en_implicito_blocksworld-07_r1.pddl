(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f g - block
  )
  (:init
    (handempty)
    (ontable d)
    (on a d)
    (clear a)
    (ontable f)
    (on e f)
    (on g e)
    (on c g)
    (on b c)
    (clear b)
  )
  (:goal
    (and
      (on e b)
      (on b f)
      (on f d)
      (on d a)
      (on a c)
      (on c g)
    )
  )
)
