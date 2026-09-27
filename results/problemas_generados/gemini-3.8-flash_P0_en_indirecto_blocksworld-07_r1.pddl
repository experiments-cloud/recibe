(define (problem blocks-7-0)
  (:domain BLOCKS)
  (:objects
    a b c d e f g - block
  )
  (:init
    (handempty)
    (clear a)
    (on a d)
    (ontable d)
    (clear b)
    (on b c)
    (on c g)
    (on g e)
    (on e f)
    (ontable f)
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
